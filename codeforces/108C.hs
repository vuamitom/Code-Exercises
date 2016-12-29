import Control.Monad

put x l i = fl ++ (x:(tail ll))
    where (fl, ll) = splitAt i l 
    
po l = map read $ words l :: [Int]
s1 :: [[Int]] -> Int -> [[Int]]
s1 x n = s x (take n (repeat []))
    where 
        s [] r = r 
        s (x:y) r = s y (put x r ((head x) - 1))

s2 x = s3 x []
    where 
        s3 x r
            | (length r) == (length x) = r
            | otherwise 
main = do
    l1 <- getLine
    let x = po l1
    let n = head x
    let p = last x
    ip <- replicateM p getLine
    let ipn = map po ip
    print (s1 ipn n)
