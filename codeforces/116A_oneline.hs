main = interact $ show . maximum . scanl (+) 0 . map ((\[x, y] -> y - x) . map read . words) . tail . lines

