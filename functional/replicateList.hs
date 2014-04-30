f n arr = foldl (\acc x -> acc ++ [x | _ <- [1..n]]) [] arr
main = do 
    n <- readLn :: IO Int 
    inputdata <- getContents 
    mapM_ putStrLn $map show $ f n $ map (read:: String -> Int) $ lines inputdata
