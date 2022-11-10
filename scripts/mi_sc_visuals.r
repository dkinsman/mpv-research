library(TDA)
library(tidyverse)

df = read.csv(file = 'raw/mpv-data.csv')
states = 
mi = df %>% filter(state == "MI") %>% subset(select = c('latitude','longitude'))
coords = cbind(mi$longitude, mi$latitude)

FltAlphaComplex <- alphaComplexFiltration(X = coords, printProgress = TRUE)
# plot alpha complex filtration
jpeg(filename = 'output/mi_alpha_vis.jpeg')
lim <- c( -90, -80, 41,48)
plot(NULL, type = "n", xlim = lim[1:2], ylim = lim[3:4],
     main = "Alpha Complex Filtration Plot (MI)")
for (idx in seq(along = FltAlphaComplex[["cmplx"]])) {
  polygon(FltAlphaComplex[["coordinates"]][FltAlphaComplex[["cmplx"]][[idx]], , drop = FALSE],
          col = "pink", border = NA, xlim = lim[1:2], ylim = lim[3:4])
}
for (idx in seq(along = FltAlphaComplex[["cmplx"]])) {
  polygon(FltAlphaComplex[["coordinates"]][FltAlphaComplex[["cmplx"]][[idx]], , drop = FALSE],
          col = NULL, xlim = lim[1:2], ylim = lim[3:4])
}  
points(FltAlphaComplex[["coordinates"]], pch = 16)


FltRips <- ripsFiltration(X = coords, maxdimension = 2,
                          maxscale = 2, dist = "euclidean", library = "GUDHI",
                          printProgress = TRUE)
dev.off()

# plot rips filtration
# WIP, session currently aborts

# plot(NULL, type = "n", xlim = lim[1:2], ylim = lim[3:4],
#      main = "Rips Filtration Plot")
# for (idx in seq(along = FltRips[["cmplx"]])) {
#   polygon(FltRips[["coordinates"]][FltRips[["cmplx"]][[idx]], , drop = FALSE],
#           col = "pink", border = NA, xlim = lim[1:2], ylim = lim[3:4])
# }
# for (idx in seq(along = FltRips[["cmplx"]])) {
#   polygon(FltRips[["coordinates"]][FltRips[["cmplx"]][[idx]], , drop = FALSE],
#           col = NULL, xlim = lim[1:2], ylim = lim[3:4])
# }  
# points(FltRips[["coordinates"]], pch = 16)

