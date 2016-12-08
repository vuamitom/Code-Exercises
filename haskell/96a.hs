import Data.List
p b|b="YES"|1>0="NO"
main=interact$p.any((>6).length).group
