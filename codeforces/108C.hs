--ghc 8.0.1 /opt/ghc/8.0.1/lib/ghc-8.0.0.20160127/

import Control.Monad

put x l i = fl ++ (x:(tail ll))
    where (fl, ll) = splitAt i l

po l = map read $ words l :: [Int]
s1 :: [[Int]] -> Int -> [[Int]]
s1 x n = s x (take n (repeat []))
    where
        s [] r = r
        s (x:y) r = s y (put x r ((head x) - 1))
        
d :: [Int] -> [[Int]] -> ([Int], [[Int]])
d (x:y:z:[]) r
    | (r!!(y-1)) == [] = ((x:y:z:[]), r)
    | x == y = ((x:y:z:[]), r)
    | otherwise = d (x:(a!!1):(minimum $ z:[(last a)]):[]) (put [] r (y-1))
        where a = r!!(y-1)
dig :: Int -> [[Int]] -> [[Int]]        
dig n x = put xs ys n
    where (xs, ys) = d (x!!n) x

solve x = s2 0 x
    where
        s2 i x
            | i == (length x) = x
            | (x!!i) == [] = s2 (i +1) x
            | otherwise = s2 (i+1) (dig i x)
solve_r x = s3 ((length x) - 1) x
    where
        s3 i x
            | i == -1 = x
            | (x!!i) == [] = s3 (i -1) x
            | otherwise = s3 (i-1) (dig i x)

--co x = [i | i <- x, not (i == [])]
co x = [i | i <- x, (not (i == [])) && (not ((i!!0) ==(i!!1)))]
pp (x:y:z:[]) = (show x) ++ " " ++ (show y) ++ " " ++ (show z)
main = do
    l1 <- getLine
    let x = po l1
    let n = head x
    let p = last x
    ip <- replicateM p getLine
    let ipn = map po ip
    let t = (s1 ipn n)
    let m = co. solve_r . solve $ dig 0 t
    print (length m)
    mapM_ (putStrLn.pp) m
