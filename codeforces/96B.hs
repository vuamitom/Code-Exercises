check [] = 0
check (x:y)
    | (fst x) == (snd x) = check y
    | (fst x) > (snd x) = 1
    | otherwise = -1
gt [] [] = 0
gt a b = check (zip a b)
        
gen l = take (l `div` 2) (repeat '4') ++ take (l `div` 2) (repeat '7')
genI l = take (l `div` 2) (repeat 4) ++ take (l `div` 2) (repeat 7)
brk x= [read (i:[]) :: Int | i <-x]

s :: [Int] -> Int -> Int -> [Int] -> [Int] -> [Int]
s [] _ _ r1 r2
    | (gt r1 r2) == -1 = []
    | otherwise = r1 
    
s (x:y) c4 c7 r1 r2
    | (d == 1) && (c4 > 0) = a
    | (d == 1) = b
    | (d == -1) = []
    | (x < 4) && (c4 > 0) = a
    | (x == 4) && (c4 > 0) && ((length a) > 0) = a
    | (x == 4) && (c7 > 0) && ((length b) > 0) = b
    | (c7 > 0) = b
    | otherwise = []
    where
        d = (gt r1 r2)
        a = s y (c4-1) c7 (r1++[4]) (r2++[x])
        b = s y c4 (c7-1) (r1++[7]) (r2++[x])

fix [] l = genI (l+2)
fix x l = x

f s = [(show x)!!0 | x <- s]
so x
    | (head x) > 7 = gen ((length x) + 2)
    | (head x) < 4 = gen (length x)    
    | ((head x) > 4) && ((head x) < 7) = "7"++ (take ((length x) `div` 2) (repeat '4')) ++  (take (((length x) `div` 2) - 1) (repeat '4'))
    | otherwise = f (fix (s x l l [] []) (length x))
        where l = ((length x) `div` 2)
sol x
    | (mod (length x) 2) == 1 = gen ((length x) + 1)
    | otherwise = so x
main = interact $  sol. brk. head . lines
