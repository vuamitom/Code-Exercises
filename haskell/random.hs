import Data.List

a 1 = "1"
a 2 = "2"
a x = "YES"

s [] = 0
s (x:y) = x + s y
len [] = 0
len (x:y) = 1 + len y 
f [] a c = a
f (x:y) a c
  | x == tail c = f y a x:c
  | otherwise = (f y c:a [])

g [] = []
g (x:y) = f y [] x:[]

main=interact$a.any((>6).length).group
--main = interact $a.len.g
--main = interact $ a

