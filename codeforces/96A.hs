import Data.List
main = interact $ \x -> if isInfixOf "0000000" x || isInfixOf "1111111" x then "YES" else "NO"
