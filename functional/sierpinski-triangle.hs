type Row = [Char]
type Matrix = [Row]


fill::  Int -> Row -> Int -> Int -> Int -> Int-> Row 
fill 63 r s b d pad 
    | s > (length r - pad) = r 
    | otherwise = fill 63 [ if inrange $ snd p then '1' else  fst p | p <- pairs ] (s + b + d ) b d pad 
    where
    pairs = zip r [0..]
    inrange x = x >= s && x < (s + b) 
   
fill w r s b d pad 
    | s > (length r - pad) = r 
    | otherwise = fill w [ got p | p <- pairs ] (s + b + d ) b d pad 
    where
    got x = if snd x >= s && snd x <( s+b+d) then update x else fst x
    update x = if (inrange $ snd x) && fst x == '1' then '1' else '_'
    pairs = zip r [0..]
    inrange x = x >= s && x < (s + b) 

initM :: Matrix 
initM = [r | _ <- [1..32]]
    where r = ['_' | _ <- [1..63]]

fillMatrix :: Matrix -> Int ->  Matrix 
fillMatrix m n = [fill n (snd p) (start $ fst p ) ( base $ fst p) ( distance (fst p)) (start $ fst p) | p <- ( withIdx  m)]  
--fillMatrix m n = [show ( distance $ fst p) | p <- ( withIdx  m)]  
    where 
        start = (+) 0 
        base x = n - (x `mod` ((n+1) `div` 2)) *2   
        distance x = 1 + (x `mod` (n+1)) * 2    
        withIdx = zip [0..] 
width 0 = 63
width n = (width 0 -1 ) `div` (2 ^n) 

reverseM = foldl (\acc x -> x : acc ) [] 

prLs [] = putStr "" 
prLs (x:xs) = do {putStrLn x; prLs xs; }

superFill m n t = if t <n then superFill h n (t+1) else h where h = fillMatrix m  (width t)
solve n = superFill (initM) n 0
main = do 
    n <- readLn :: IO Int
    --print $ width n
    --prLs $reverseM $ fillMatrix ( initM ) (width n)  
    prLs $reverseM $ solve n 
    --print $ fill ['_' | _<- [1..63]] 1 13 3 
    
