-- ตารางอันดับ: ผู้เล่นทุกคนอ่านได้ แต่เขียนได้ผ่านฟังก์ชัน submit_score เท่านั้น
create table public.leaderboard (
  user_id uuid not null references auth.users(id) on delete cascade,
  board text not null,
  period text not null,
  score bigint not null,
  name text not null default 'ผู้กล้า',
  hero text,
  detail jsonb,
  updated_at timestamptz not null default now(),
  primary key (user_id, board, period)
);
create index leaderboard_rank on public.leaderboard (board, period, score desc);
alter table public.leaderboard enable row level security;
grant select on public.leaderboard to anon, authenticated;
create policy "anyone can read leaderboard" on public.leaderboard
  for select to anon, authenticated using (true);

create or replace function public.submit_score(p_board text, p_period text, p_score bigint, p_name text, p_hero text, p_detail jsonb)
returns void language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); cap bigint; last timestamptz;
begin
  if uid is null then raise exception 'not logged in'; end if;
  cap := case p_board when 'endless' then 50000000 when 'daily' then 50000000
                      when 'hundred' then 100 when 'dragon' then 1000000000000 else null end;
  if cap is null then raise exception 'bad board'; end if;
  if p_score < 0 or p_score > cap then raise exception 'score out of range'; end if;
  if p_board in ('endless','hundred') and p_period <> 'all' then raise exception 'bad period'; end if;
  select updated_at into last from leaderboard where user_id = uid and board = p_board and period = p_period;
  if last is not null and last > now() - interval '3 seconds' then raise exception 'too fast'; end if;
  insert into leaderboard (user_id, board, period, score, name, hero, detail, updated_at)
  values (uid, p_board, p_period, p_score, left(coalesce(nullif(trim(p_name),''),'ผู้กล้า'), 20), left(p_hero, 30), p_detail, now())
  on conflict (user_id, board, period) do update set
    score = greatest(leaderboard.score, excluded.score),
    name = excluded.name,
    hero = excluded.hero,
    detail = case when excluded.score > leaderboard.score then excluded.detail else leaderboard.detail end,
    updated_at = now();
end $$;
revoke all on function public.submit_score(text, text, bigint, text, text, jsonb) from public, anon;
grant execute on function public.submit_score(text, text, bigint, text, text, jsonb) to authenticated;

create or replace function public.my_rank(p_board text, p_period text)
returns table (rank bigint, score bigint, total bigint)
language sql stable security definer set search_path = public as $$
  select (select count(*) + 1 from leaderboard l where l.board = p_board and l.period = p_period and l.score > me.score),
         me.score,
         (select count(*) from leaderboard l where l.board = p_board and l.period = p_period)
  from leaderboard me
  where me.user_id = auth.uid() and me.board = p_board and me.period = p_period;
$$;
revoke all on function public.my_rank(text, text) from public, anon;
grant execute on function public.my_rank(text, text) to authenticated;
