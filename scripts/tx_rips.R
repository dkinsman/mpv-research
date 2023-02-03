library(TDA)
library(tidyverse)
library(maps)

df = read.csv(file = 'raw/mpv-data.csv')
states = 
  tx = df %>% filter(state == "TX") %>% subset(select = c('latitude','longitude'))
coords = cbind(tx$longitude, tx$latitude)

FltRipsComplex <- ripsFiltration(X = coords, maxdimension = 1, maxscale = 0.25, dist = 'euclidean',
                                 library = 'GUDHI', printProgress = TRUE)
rips_dgm <- ripsDiag(coords, 2, 0.25, dist = 'euclidean')

# plot alpha complex filtration
png(filename = 'output/tx_rips_vis.png', width = 5, height = 6, units= 'in', res = 1200)
lim <- map('state', 'Texas', plot=FALSE)$range
plot(NULL, type = "n", xlim = lim[1:2], ylim = lim[3:4],
     main = "Rips Complex Filtration Plot (MI)", xlab = 'Longitute', ylab = 'Ladtitude')
for (idx in seq(along = FltRipsComplex[["cmplx"]])) {
  polygon(FltRipsComplex[["coordinates"]][FltRipsComplex[["cmplx"]][[idx]], , drop = FALSE],
          col = rgb(0, 0,1, 0.1), border = NA, xlim = lim[1:2], ylim = lim[3:4])
}
for (idx in seq(along = FltRipsComplex[["cmplx"]])) {
  polygon(FltRipsComplex[["coordinates"]][FltRipsComplex[["cmplx"]][[idx]], , drop = FALSE],
          col = NULL, lwd = 0.25, xlim = lim[1:2], ylim = lim[3:4])
}  
map('state', 'Texas', add=T)
points(FltRipsComplex[["coordinates"]], pch = 16, cex = 0.20, col = rgb(0,0,0,0.40))
dev.off()
