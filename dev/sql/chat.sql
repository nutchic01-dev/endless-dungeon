-- ระบบแชทโลก: ทุกคนอ่านได้ (ข้อความ 3 วันล่าสุด) ส่งได้เฉพาะคนที่เข้าสู่ระบบ ผ่านฟังก์ชัน send_chat เท่านั้น
create table if not exists public.chat_messages (
  id bigserial primary key,
  user_id uuid not null references auth.users(id) on delete cascade,
  channel text not null default 'world',
  name text not null default 'ผู้กล้า',
  hero text,
  body text not null check (char_length(body) between 1 and 200),
  created_at timestamptz not null default now()
);
create index if not exists chat_messages_recent on public.chat_messages (channel, id desc);
alter table public.chat_messages enable row level security;
grant select on public.chat_messages to anon, authenticated;
grant usage, select on sequence public.chat_messages_id_seq to authenticated;
drop policy if exists "read recent chat" on public.chat_messages;
create policy "read recent chat" on public.chat_messages
  for select to anon, authenticated using (created_at > now() - interval '3 days');

create or replace function public.send_chat(p_body text, p_name text, p_hero text)
returns bigint language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); last timestamptz; n int; b text; new_id bigint;
begin
  if uid is null then raise exception 'not logged in'; end if;
  b := left(regexp_replace(trim(coalesce(p_body,'')), '\s+', ' ', 'g'), 200);
  if char_length(b) = 0 then raise exception 'empty message'; end if;
  select max(created_at) into last from chat_messages where user_id = uid;
  if last is not null and last > now() - interval '3 seconds' then raise exception 'chat too fast'; end if;
  select count(*) into n from chat_messages where user_id = uid and created_at > now() - interval '1 minute';
  if n >= 12 then raise exception 'chat too fast'; end if;
  insert into chat_messages (user_id, channel, name, hero, body)
  values (uid, 'world', left(coalesce(nullif(trim(p_name),''),'ผู้กล้า'), 20), left(p_hero, 30), b)
  returning id into new_id;
  if new_id % 50 = 0 then delete from chat_messages where created_at < now() - interval '3 days'; end if;
  return new_id;
end $$;
revoke all on function public.send_chat(text, text, text) from public, anon;
grant execute on function public.send_chat(text, text, text) to authenticated;
notify pgrst, 'reload schema';
