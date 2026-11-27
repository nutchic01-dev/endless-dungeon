-- สนามประลองวีรชน: ทีมป้องกันของผู้เล่น + บันทึกผลการประลอง (รันซ้ำได้)
create table if not exists public.arena_teams (
  user_id uuid primary key references auth.users(id) on delete cascade,
  name text not null default 'ผู้กล้า',
  rating int not null default 1000,
  power bigint not null default 0,
  team jsonb not null,
  wins int not null default 0,
  losses int not null default 0,
  updated_at timestamptz not null default now()
);
create index if not exists arena_teams_rating on public.arena_teams (rating desc);
alter table public.arena_teams enable row level security;
grant select on public.arena_teams to anon, authenticated;
drop policy if exists "anyone can read arena teams" on public.arena_teams;
create policy "anyone can read arena teams" on public.arena_teams for select to anon, authenticated using (true);

create table if not exists public.arena_log (
  id bigserial primary key,
  attacker uuid not null references auth.users(id) on delete cascade,
  defender uuid references auth.users(id) on delete cascade,
  att_name text,
  win boolean not null,
  delta int not null,
  created_at timestamptz not null default now()
);
create index if not exists arena_log_att on public.arena_log (attacker, created_at desc);
create index if not exists arena_log_def on public.arena_log (defender, id desc);
alter table public.arena_log enable row level security;
grant select on public.arena_log to authenticated;
drop policy if exists "see own arena log" on public.arena_log;
create policy "see own arena log" on public.arena_log for select to authenticated using (attacker = auth.uid() or defender = auth.uid());

-- บันทึก/อัปเดตทีมป้องกัน (คะแนนเดิมไม่เปลี่ยน)
create or replace function public.arena_set(p_name text, p_team jsonb, p_power bigint)
returns table (rating int) language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid();
begin
  if uid is null then raise exception 'not logged in'; end if;
  if jsonb_typeof(p_team) <> 'array' or jsonb_array_length(p_team) < 1 or jsonb_array_length(p_team) > 5 then raise exception 'bad team'; end if;
  if octet_length(p_team::text) > 4000 then raise exception 'bad team'; end if;
  insert into arena_teams (user_id, name, team, power, updated_at)
  values (uid, left(coalesce(nullif(trim(p_name),''),'ผู้กล้า'),20), p_team, greatest(0, least(p_power, 1000000000)), now())
  on conflict (user_id) do update set name = excluded.name, team = excluded.team, power = excluded.power, updated_at = now();
  return query select a.rating from arena_teams a where a.user_id = uid;
end $$;
revoke all on function public.arena_set(text, jsonb, bigint) from public, anon;
grant execute on function public.arena_set(text, jsonb, bigint) to authenticated;

-- ส่งผลการประลอง: p_opp = null เมื่อสู้กับบอท (ได้/เสียคะแนนครึ่งเดียว)
create or replace function public.arena_report(p_opp uuid, p_win boolean)
returns table (rating int, delta int) language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); my_r int; my_name text; op_r int; e float8; d int; n int;
begin
  if uid is null then raise exception 'not logged in'; end if;
  select a.rating, a.name into my_r, my_name from arena_teams a where a.user_id = uid;
  if my_r is null then raise exception 'set defense first'; end if;
  if p_opp = uid then raise exception 'bad opponent'; end if;
  select count(*) into n from arena_log l where l.attacker = uid and l.created_at > now() - interval '1 day';
  if n >= 12 then raise exception 'too many'; end if;
  if exists (select 1 from arena_log l where l.attacker = uid and l.created_at > now() - interval '6 seconds') then raise exception 'too fast'; end if;
  if p_opp is not null then
    select a.rating into op_r from arena_teams a where a.user_id = p_opp;
    if op_r is null then raise exception 'bad opponent'; end if;
    e := 1.0 / (1.0 + power(10.0, (op_r - my_r) / 400.0));
    d := round(24 * (case when p_win then 1 - e else -e end));
  else
    d := round(12 * (case when p_win then 0.5 else -0.5 end));
  end if;
  update arena_teams a set rating = greatest(0, a.rating + d),
    wins = a.wins + (case when p_win then 1 else 0 end), losses = a.losses + (case when p_win then 0 else 1 end)
  where a.user_id = uid;
  if p_opp is not null then
    update arena_teams a set rating = greatest(0, a.rating - round(d * 0.5)::int) where a.user_id = p_opp;
  end if;
  insert into arena_log (attacker, defender, att_name, win, delta) values (uid, p_opp, my_name, p_win, d);
  return query select a.rating, d from arena_teams a where a.user_id = uid;
end $$;
revoke all on function public.arena_report(uuid, boolean) from public, anon;
grant execute on function public.arena_report(uuid, boolean) to authenticated;
notify pgrst, 'reload schema';
