library(TDA)
library(tidyverse)
library(maps)

df = read.csv(file = 'raw/mpv-data.csv')
states = 
  tx = df %>% filter(state == "TX") %>% subset(select = c('latitude','longitude'))
coords = cbind(tx$longitude, tx$latitude)

FltAlphaComplex <- alphaComplexFiltration(X = coords, printProgress = TRUE)
# plot alpha complex filtration
png(filename = 'output/tx_alpha_vis.png', width = 5, height = 6, units= 'in', res = 1200)
lim <- map('state', 'Texas', plot=FALSE)$range
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
map('state', 'Texas', add=T)
points(FltAlphaComplex[["coordinates"]], pch = 16, cex = 0.40, col = rgb(0,0,0,0.40))
dev.off()

