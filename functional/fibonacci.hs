-- tail recursion 
-- seem like Haskell has some optimization for this 
-- cause not only it take less space but also less time
module Main where
f 1 x  = x 
f 2 x = 1 + x 
f n x = f (n-1) y where y = f (n-2) x 
fib n = f n 0 
  
    
main = do
    input <- getLine 
    print . fib . (read :: String -> Int) $input 
