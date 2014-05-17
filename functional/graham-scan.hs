import Text.Printf

ccw p1 p2 p3 = (fst p2 - fst p1) * (snd p3 - snd p1) - (snd p2 - snd p1) * (fst p3 - fst p1)

lowest :: [(Int, Int)] ->(Int, Int)
lowest (x:xs) = low xs x 
    where
    low [] a = a
    low (y:ys) a = if snd a < snd y then low ys a else low ys y 

solveM [] hull = hull 
solveM (a:as) (x:y:ys) = if isLeft x y a then solveM as a:(_) else solveM (_) y:ys  
    where isLeft x y a = ccw x y a > 0 

solve :: [(Int, Int)] -> Double
solve points = lp   
    where 
    lp = lowest points 
    other = [p | p <- points , fst p != fst lp && snd p!= snd lp ] 
    init (x:y:xs) = x:y:[]

main :: IO ()
main = do
    n <- readLn :: IO Int
    content <- getContents
    let  
        points = map (\[x, y] -> (x, y)). map (map (read::String->Int)). map words. lines $ content
        ans = solve points
     printf "%.1f\n" ans
