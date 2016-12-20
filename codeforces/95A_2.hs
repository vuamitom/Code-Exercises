--ghc 8.0.1 /opt/ghc/8.0.1/lib/ghc-8.0.0.20160127/

import Control.Monad
import Data.List
import Data.Char (isSpace, toLower, toUpper)
rstrip x = [a | a <- x, not (isSpace a)]
takeR :: Int -> [Char] -> [Char]
takeR n s = go (take n (repeat 1)) s
    where
        go [] r = r 
        go (_:x) (_:y) = go x y 
        
lower x = [toLower y | y <- x]

sw c t
    | c > 'Z'&& t < 'a' = toLower t
    | c < 'a' && t > 'Z' = toUpper t
    | otherwise = t
    
make :: [Char] -> Char -> [Char]
make s t = [(sw c t)|c <- s]

replace :: [Char] -> [Char] -> Char -> String
replace x fw l
    | (length x) == 0 = x
    | (length x) < (length fw) = x
    | (lower (take (length fw) x)) == (lower fw) = (make (take (length fw) x) l) ++ (replace (takeR (length fw) x) fw l)
    | otherwise = ((head x):[]) ++ replace (tail x) fw l
    
cb :: (Char, Char) -> Char -> Char
cb c l
    | fst c == l = l
    | snd c == l = l
    | otherwise = fst c
combine :: [String] -> Char -> String
combine s l = comb s l (take (length (last s)) (repeat ' '))
    where
        comb [] l r = r 
        comb (x:y) l r = comb y l [(cb c l)|c<-(zip x r)]
    
main = do
    n <- getLine
    fw <- replicateM (read n) getLine    
    ip <- getLine
    letter <-getLine
    
    let fww = [rstrip x | x <- fw] 
--    print (last fww)
    --let x = (replace (rstrip ip) (last fww) 't')
    --let y = (replace (rstrip ip) (head fww) 't')
    --let l = last letter
    --let t = [(cb c l) | c <- (zip x (take (length (rstrip ip)) (repeat ' ')))]
    --print t
    --print x 
    --print y
    --let t2 = [(cb c l) | c <- (zip t y)]
    --print t2
    --let t3 = make "eLu" 't'
    --print t3
    --let m = combine (["aaaaa", "bbbbb"]) (last letter)
    let m = combine [(replace (rstrip ip) w (last letter)) | w <- fww] (last letter)
    print m

