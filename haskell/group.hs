f :: [Char] -> [[Char]] -> [[Char]]
f [] a = a
f (x:y) [] = f y [[x]] 
f (x:y) a
  | x == last (last a) = f y ((init a) ++ (x:(last a)):[])
  | otherwise = f y (a ++[[x]])
len x = sum [1 | _ <- x]  
