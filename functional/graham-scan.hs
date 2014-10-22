import Text.Printf

ccw p1 p2 p3 = (fst p2 - fst p1) * (snd p3 - snd p1) - (snd p2 - snd p1) * (fst p3 - fst p1)

lowest :: [(Int, Int)] ->(Int,Int)
lowest (x:xs) = low xs x 
    where
    low [] a = a
    low (y:ys) a = if snd a < snd y then low ys a else low ys y 

swap ar = lw : [a | a <- ar, fst a /= (fst lw) && snd a/= (snd lw)]    where 
    lw = lowest ar

colinearCompare l a b = if dist l a >= dist l b then -1 else 1 
    where 
    dist x y = sq (fst x - fst y) + sq (snd x - snd y)
    sq r = r * r

compareG ::(Int, Int)-> (Int, Int) ->(Int, Int)-> Int
compareG l a b = if cc == 0 then colinearCompare l a b else translate cc 
    where 
    cc = ccw l a b 
    translate x = if x > 0 then -1 else 1 
     

sortG all@(x:xs) = x : ( sortO xs (compareG $ lowest all) )
sortO ::[(Int, Int)] -> ((Int, Int) -> (Int, Int)->Int) -> [(Int, Int)]
sortO [] _ = []
sortO (a:as) comp = (sortO le comp) ++ [a] ++ (sortO mo comp)
    where 
    le = [b | b <- as ,comp a b <= 0  ] 
    mo = [c | c<-as, comp a c > 0] 
    
solveG (x:y:z:ts) = solveM ts [x,y,z] 

solveM :: [(Int, Int)] -> [(Int, Int)] -> [(Int, Int)]
solveM [] hull = hull 
solveM remain@(a:as) hull@(x:y:ys) = if isLeft x y a then solveM as (a:hull) else solveM remain (y:ys) -- TODO : check for case when ys has only 1 elemnt 
    where isLeft x y a = ccw x y a > 0 


solve :: [(Int, Int)] -> Int
solve points = 11   
--    where 
--    lp = 111 
--    other = [p | p <- points , fst p /= fst lp && snd p/= snd lp ] 
--    init (x:y:xs) = x:y:[]

main :: IO ()
main = do
    n <- readLn :: IO Int
    content <- getContents
    let  
        points = map (\[x, y] -> (x, y)). map (map (read::String->Int)). map words. lines $ content
        ans = solve points
    putStrLn $ show $ccw (1,1) (2,5) (2,2)
    -- MAKE BELOW CASE WORKS
    putStrLn $ show $ solveG [(1,1),(2,2),(2,5),(3,3),(3,2),(5,3)]
    putStrLn $  show $ solveG $ sortG $ swap [(2,5), (1,1),(3,3),(5,3),(3,2),(2,2)]
    --printf "%.1f\n" ans
