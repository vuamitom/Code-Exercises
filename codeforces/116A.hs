import Control.Monad
split [] r = r
split (x:y) r 
    | not (x == ' ') =  split y ((init r) ++ [(last r) ++ [x]])
    | otherwise = split y (r ++ [""])
toInt r = [read x::Int | x <- r]

go :: [[Int]] -> Int -> [Int] ->[Int]
go [] x y = y
go (r1:r2) x y = go r2 (x - (r1!!0) + (r1!!1)) ((x - (r1!!0) + (r1!!1)):y)
solve :: [[Int]] -> [Int]
solve r = go r 0 []

        
main = do
    nn <- getLine
    let n = read nn :: Int
    ip <- replicateM n getLine
    --print ip
    let ip2 = [toInt (split x [""]) | x <- ip]
    --print ip2
    let r = solve ip2
    print (maximum r)
