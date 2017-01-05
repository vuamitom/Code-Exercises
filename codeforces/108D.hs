fact n = f n 1
    where 
        f 0 r = r
        f n r = f (n - 1) (r * n)        

comb :: Int -> Int -> Int
comb n 0 = 1
comb n k = (fact n) `div` ((fact k) * (fact $ n - k ))
toI l = map read $ words l :: [Int]

pos n s h = sum [(comb h i) * (comb s (n - i)) | i <- p]
    where 
        m = max [n, h] 
        p = [1..h]
        
solve n s h
    | n > s = -1 
    | h == 1 = 0
    | n == s = 1
    | otherwise = (fromIntegral (pos (n - 1) (s - h) (h -1))) / (fromIntegral  (comb (s - 1) (n - 1)))

main = do 
    l1 <- getLine 
    let [n, m, h] = toI l1
    l2 <- getLine 
    let s = toI l2 
    print $ sum s
    print $ fact 24
    print $ fact 5
    print $ fact 19
    print $ comb 24 5
    --print $ solve n (sum s) (s!!(h-1))
