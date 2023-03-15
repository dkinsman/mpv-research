library(TDA)
library(tidyverse)
library(maps)

df = read.csv(file = 'raw/mpv-data.csv')
states = 
mi = df %>% filter(state == "MI") %>% subset(select = c('latitude','longitude'))
coords = cbind(mi$longitude, mi$latitude)

clusters <- c(data.frame(x = c(-83.0458, -85.5872, -83.6875,-85.6681), 
                         y = c(42.3314, 42.2917, 43.0125, 42.9634),
                         z = c('Detroit', 'Kalamazoo', 'Flint', 'Grand Rapids')))

FltRipsComplex <- ripsFiltration(X = coords, maxdimension = 1, maxscale = 0.25, dist = 'euclidean',
                                 library = 'GUDHI', printProgress = TRUE)
# plot alpha complex filtration
png(filename = 'output/mi_rips_vis.png', width = 5, height = 6, units= 'in', res = 300)
lim <- map('state', 'Michigan', plot=FALSE)$range
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
map('state', 'Michigan', add=T)
points(FltRipsComplex[["coordinates"]], pch = 16, cex = 0.20, col = rgb(0,0,0,0.40))
#for the clusters to be plotted
#points(clusters, pch = 16, cex = 0.65, col = rgb(0.85,0,0.15))
#text(clusters$x, clusters$y-0.15, labels = clusters$z, cex = 0.65, col = rgb(0.85,0,0.15))
dev.off()
