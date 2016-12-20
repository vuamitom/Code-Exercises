--ghc 8.0.1 /opt/ghc/8.0.1/lib/ghc-8.0.0.20160127/
import Data.Char
strip x = [c | c <- x, not ((c == '"') || (c == '\r'))]

isP :: Int -> Int -> Int -> Int
isP n k x
    | 0 < (mod n k) = -1
    | 1 == (div n k) = x + 1
    | otherwise = isP (div n k) k (x + 1)
sol x
    | x >= 0 = "YES\n" ++ (show x)
    | otherwise = "NO"

main = do
    p <- getLine 
    n <- getLine 
    let x = read . strip $ p 
    let y = read. strip $ n
    let r = isP y x (-1)
    putStrLn . sol $ r
    


