library(TDA)
library(tidyverse)
library(maps)

df = read.csv(file = 'raw/mpv-data.csv')
states = 
mi = df %>% filter(state == "MI") %>% subset(select = c('latitude','longitude'))
coords = cbind(mi$longitude, mi$latitude)

FltAlphaComplex <- alphaComplexFiltration(X = coords, printProgress = TRUE)
# plot alpha complex filtration
png(filename = 'output/mi_alpha_vis.png', width = 4, height = 4, units= 'in', res = 1000)
lim <- map('state', 'Michigan', plot=FALSE)$range
plot(NULL, type = "n", xlim = lim[1:2], ylim = lim[3:4],
     main = "Alpha Complex Filtration Plot (MI)", xlab = 'Longitute', ylab = 'Ladtitude')
for (idx in seq(along = FltAlphaComplex[["cmplx"]])) {
  polygon(FltAlphaComplex[["coordinates"]][FltAlphaComplex[["cmplx"]][[idx]], , drop = FALSE],
          col = rgb(0, 0,1, 0.1), border = NA, xlim = lim[1:2], ylim = lim[3:4])
}
for (idx in seq(along = FltAlphaComplex[["cmplx"]])) {
  polygon(FltAlphaComplex[["coordinates"]][FltAlphaComplex[["cmplx"]][[idx]], , drop = FALSE],
          col = NULL, lwd = 0.25, xlim = lim[1:2], ylim = lim[3:4])
}  
map('state', 'Michigan', add=T)
points(FltAlphaComplex[["coordinates"]], pch = 16, cex = 0.40, col = rgb(0,0,0,0.40))
dev.off()

FltRips <- ripsFiltration(X = coords, maxdimension = 2,
                          maxscale = 2, dist = "euclidean", library = "GUDHI",
                          printProgress = TRUE)

# plot rips filtration
# WIP, session currently aborts
# png(filename = 'output/mi_rips_vis.png', width = 4, height = 4, units= 'in', res = 1000)
# plot(NULL, type = "n", xlim = lim[1:2], ylim = lim[3:4],
#      main = "Rips Filtration Plot")
# for (idx in seq(along = FltRips[["cmplx"]])) {
#   polygon(FltRips[["coordinates"]][FltRips[["cmplx"]][[idx]], , drop = FALSE],
#           col = "pink", border = NA, xlim = lim[1:2], ylim = lim[3:4])
# }
# for (idx in seq(along = FltRips[["cmplx"]])) {
#   polygon(FltRips[["coordinates"]][FltRips[["cmplx"]][[idx]], , drop = FALSE],
#           col = NULL, lwd = 0.25, xlim = lim[1:2], ylim = lim[3:4])
# }
# points(FltRips[["coordinates"]], pch = 16, cex = 0.40, col = rgb(0,0,0,0.40))
# dev.off()
