-- ระบบแอดมินในแชท: ป้าย 👑 ADMIN ที่ปลอมไม่ได้ (เช็กจากบัญชีบนเซิร์ฟเวอร์) + แอดมินลบข้อความได้
-- ⚠️ ก่อนรัน: แก้อีเมลในบรรทัด "ตั้งตัวเองเป็นแอดมิน" ด้านล่าง ให้เป็นอีเมลที่ใช้เข้าสู่ระบบในเกม

create table if not exists public.chat_admins (
  user_id uuid primary key references auth.users(id) on delete cascade
);
alter table public.chat_admins enable row level security;   -- ไม่เปิดให้ใครอ่าน/เขียนตรง ๆ

alter table public.chat_messages add column if not exists is_admin boolean not null default false;

-- ส่งข้อความ: ติดป้ายแอดมินให้อัตโนมัติ และกันคนทั่วไปตั้งชื่อเลียนแบบแอดมิน
create or replace function public.send_chat(p_body text, p_name text, p_hero text)
returns bigint language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); last timestamptz; n int; b text; nm text; adm boolean; new_id bigint;
begin
  if uid is null then raise exception 'not logged in'; end if;
  adm := exists(select 1 from chat_admins where user_id = uid);
  b := left(regexp_replace(trim(coalesce(p_body,'')), '\s+', ' ', 'g'), 200);
  if char_length(b) = 0 then raise exception 'empty message'; end if;
  if not adm then
    select max(created_at) into last from chat_messages where user_id = uid;
    if last is not null and last > now() - interval '3 seconds' then raise exception 'chat too fast'; end if;
    select count(*) into n from chat_messages where user_id = uid and created_at > now() - interval '1 minute';
    if n >= 12 then raise exception 'chat too fast'; end if;
  end if;
  nm := left(coalesce(nullif(trim(p_name),''),'ผู้กล้า'), 20);
  if not adm and nm ~* '(admin|แอดมิน|แอด มิน|ทีมงาน|\mgm\M|ผู้ดูแล)' then nm := 'ผู้กล้า'; end if;
  insert into chat_messages (user_id, channel, name, hero, body, is_admin)
  values (uid, 'world', nm, left(p_hero, 30), b, adm)
  returning id into new_id;
  if new_id % 50 = 0 then delete from chat_messages where created_at < now() - interval '3 days'; end if;
  return new_id;
end $$;
revoke all on function public.send_chat(text, text, text) from public, anon;
grant execute on function public.send_chat(text, text, text) to authenticated;

-- เกมใช้เช็กว่าคนที่ล็อกอินอยู่เป็นแอดมินไหม (เพื่อโชว์ปุ่มลบ)
create or replace function public.chat_is_admin()
returns boolean language sql security definer set search_path = public as $$
  select exists(select 1 from chat_admins where user_id = auth.uid());
$$;
revoke all on function public.chat_is_admin() from public, anon;
grant execute on function public.chat_is_admin() to authenticated;

-- แอดมินลบข้อความ
create or replace function public.admin_chat_delete(p_id bigint)
returns void language plpgsql security definer set search_path = public as $$
begin
  if not exists(select 1 from chat_admins where user_id = auth.uid()) then raise exception 'not admin'; end if;
  delete from chat_messages where id = p_id;
end $$;
revoke all on function public.admin_chat_delete(bigint) from public, anon;
grant execute on function public.admin_chat_delete(bigint) to authenticated;

-- ===== ตั้งตัวเองเป็นแอดมิน (แก้อีเมลให้ตรงกับบัญชีในเกม) =====
insert into public.chat_admins (user_id)
select id from auth.users where email = 'ใส่อีเมลของคุณ@gmail.com'
on conflict do nothing;

-- เช็กว่าตั้งสำเร็จ: ต้องเห็นอีเมลของคุณ 1 แถว
select u.email from public.chat_admins a join auth.users u on u.id = a.user_id;

notify pgrst, 'reload schema';
