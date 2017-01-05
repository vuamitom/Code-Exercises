toI l = map read $ words l :: [Int]
--comp s h = product [(s - h + 1) .. s]

solve n s h
    | n > s = -1
    | h == 1 = 0
    | n == s = 1
    | otherwise = 1 - ((fromIntegral a) / (fromIntegral b))
        where 
            a = product [(s - h - n  + 2)..(s - h)]
            b = product [(s-n + 1)..(s-1)]
        

main = do
    l1 <- getLine
    let [n, m, h] = toI l1
    l2 <- getLine
    let s = toI l2
    let sh = s!!(h-1)
    let ss = sum s
    --print $ comp (ss - n + 1) sh
    print $ solve n ss sh
