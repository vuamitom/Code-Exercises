--ghc 8.0.1 /opt/ghc/8.0.1/lib/ghc-8.0.0.20160127/
import Control.Monad
import Data.List
import Data.Char (isSpace)
rstrip x = [a | a <- x, not (isSpace a)]

--solve :: [Char] -> [Char] -> [[Char]] -> [[Char]] -> [Char]
--solve [] b c fw = last c
--solve (x:y) "" c fw = solve y (f x fw
--solve (x:y) b c fw = last (take ( length(c) - length(y) ) c)
cl x l = sum [1 | c <- x, c == l]

tak rip x = reverse (take ((length rip) - (length x)) (reverse rip))

m :: [Char] -> [[Char]] -> [[Char]]
m x fw = [a | a <- fw, isPrefixOf a x]
tl :: [Char] -> Char -> [Char]
tl a letter = take (length a) (repeat letter)
--solve rip fw letter = snd (maximum [(cl i, i)|i <- (map cl [(solve (take ((length x) - (length rip)) rip) fw letter) ++ (take (length x) (repeat letter)) | x <- (m rip fw)])])
solve :: [Char] -> [[Char]] -> Char -> [[Char]]
solve rip fw letter = ((head rip):[]):[tl x letter | x <- (m rip fw)]

solve2 :: [Char] -> [[Char]] -> Char -> [Char]

solve2 [] fw letter = ""
solve2 rip fw letter =   snd (maximum [(cl i letter, i) | i <- [(solve2 (tak rip x) fw letter) ++ x | x <- (solve rip fw letter)]])
--s x fw = (m x fw)
main = do
    n <- getLine
    fw <- replicateM (read n) getLine
    ip <- getLine
    letter <-getLine
    let sfw = (map reverse (map rstrip fw))
    let bg = take (length ip) (repeat [])
    let test =  (solve2 (reverse (rstrip ip)) sfw 't')
    
    let test2 = solve  (reverse "kelu") sfw 't'
    print test2
    print test
    print sfw
    


