type Row = [Char]
type Matrix = [Row]

fill::  Row -> Int -> Int -> Int -> Int-> Row 
fill r s b d pad 
    | s > (length r - pad) = r 
    | otherwise = fill [ if inrange $ snd p then '1' else  fst p | p <- pairs ] (s + b + d ) b d pad 
        where 
            pairs = zip r [0..]
            inrange x = x >= s && x < (s + b) 
initM :: Matrix 
initM = [r | _ <- [1..32]]
    where r = ['_' | _ <- [1..63]]

fillMatrix :: Matrix -> Int ->  Matrix 
fillMatrix m n = [fill (snd p) (start $ fst p ) ( base $ fst p) ( distance (fst p)) (start $ fst p) | p <- ( withIdx  m)]  
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

main = do 
    n <- readLn :: IO Int
    --print $ width n
    prLs $reverseM $ fillMatrix ( initM ) (width n)  
    --print $ fill ['_' | _<- [1..63]] 1 13 3 
    
