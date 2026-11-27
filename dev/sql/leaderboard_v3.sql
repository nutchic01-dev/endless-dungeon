-- ตารางอันดับ v3 (v3.60): เพิ่มกระดาน 'endlessw' = หอคอยไร้สิ้นสุดรายสัปดาห์ (period = เลขสัปดาห์)
-- รันซ้ำได้ ไม่ลบข้อมูลเดิม · ต้องเคยรัน leaderboard_v2.sql มาก่อน
create or replace function public.submit_score(p_board text, p_period text, p_score bigint, p_name text, p_hero text, p_detail jsonb)
returns void language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); cap bigint; last timestamptz;
begin
  if uid is null then raise exception 'not logged in'; end if;
  cap := case p_board when 'endless' then 50000000 when 'endlessw' then 50000000 when 'daily' then 50000000
                      when 'hundred' then 100 when 'dragon' then 1000000000000 else null end;
  if cap is null then raise exception 'bad board'; end if;
  if p_score < 0 or p_score > cap then raise exception 'score out of range'; end if;
  if p_board in ('endless','hundred') and p_period <> 'all' then raise exception 'bad period'; end if;
  if p_board = 'endlessw' and p_period !~ '^[0-9]{1,6}$' then raise exception 'bad period'; end if;
  if octet_length(coalesce(p_detail::text,'')) > 20000 then raise exception 'detail too large'; end if;
  select updated_at into last from leaderboard where user_id = uid and board = p_board and period = p_period;
  if last is not null and last > now() - interval '3 seconds' then raise exception 'too fast'; end if;
  insert into leaderboard (user_id, board, period, score, name, hero, detail, updated_at)
  values (uid, p_board, p_period, p_score, left(coalesce(nullif(trim(p_name),''),'ผู้กล้า'), 20), left(p_hero, 30), p_detail, now())
  on conflict (user_id, board, period) do update set
    score = greatest(leaderboard.score, excluded.score),
    name = excluded.name,
    hero = case when excluded.score >= leaderboard.score then excluded.hero else leaderboard.hero end,
    detail = case when excluded.score >= leaderboard.score then excluded.detail else leaderboard.detail end,
    updated_at = now();
end $$;
revoke all on function public.submit_score(text, text, bigint, text, text, jsonb) from public, anon;
grant execute on function public.submit_score(text, text, bigint, text, text, jsonb) to authenticated;

-- ล้างอันดับรายสัปดาห์ที่เก่ากว่า 8 สัปดาห์ (ไม่บังคับ รันเมื่อไหร่ก็ได้)
-- delete from public.leaderboard where board = 'endlessw' and period ~ '^[0-9]+$' and period::int < (select max(period::int) - 8 from public.leaderboard where board='endlessw' and period ~ '^[0-9]+$');
notify pgrst, 'reload schema';
