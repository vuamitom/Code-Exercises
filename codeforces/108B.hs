--ghc 8.0.1 /opt/ghc/8.0.1/lib/ghc-8.0.0.20160127/
import Data.List
split b = s b [""]
    where
        s "" r = r
        s x r
            | head x == ' ' = s (tail x) (r ++ [""])
            | otherwise = s (tail x) ((init r) ++ [((last r) ++ [(head x)])])
            
split2 b = s b []
    where 
        s "" r = r
        s x r
            | head x == ' ' = 
            
dedup x = d x []
    where 
        d (x:[]) r = r ++ [x]
        d (x:y) r
            | x == (head y) = d y r
            | otherwise = d y (r ++ [x])
        
sol [] = "NO"            
sol (x:[]) = "NO"
sol (x:y)
    | (2 * x) > (head y) = "YES"
    | otherwise = sol y
            
main = do 
    n0 <- getLine
    b <- getLine
    let n = read n0 :: Int
    let a = dedup (sort [read x :: Int | x <- (split b)])
    let r = sol a
    putStrLn r
