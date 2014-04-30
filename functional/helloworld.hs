hello_worlds 1 = putStrLn "Hello World" 
hello_worlds n = do {hello_words 1 ;  hello_worlds (n-1);} 
main = do 
    n <- readLn :: IO Int 
    hello_worlds n 
