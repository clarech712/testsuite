x <- rnorm(100)
hist(x, main="Random Normal Distribution", col="blue")
dev.copy(png, 'histogram.png')
dev.off()

