ok 0 0 = True
ok _ 0 = False
ok d n = if n `mod` 10 == 4
  then ok (d+1) (n `div` 10)
  else ok (d-1) (n `div` 10)

n 0 = 4
n x = if x `mod` 10 == 4
  then x + 3
  else (n $ (x `div` 10)) * 10 + 4

main = do
  s <- getLine
  print $ head $ dropWhile (< read s) $ filter (ok 0) $ iterate n 4
