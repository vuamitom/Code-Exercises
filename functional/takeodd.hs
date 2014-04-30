f lst = let pairs = zip lst [1..] in [fst x | x <- pairs , even $ snd x ]
main = do 
    inputdata <- getContents
    mapM_ putStrLn $ map show $ f $ map ( read :: String -> Int) $ lines inputdata
