x = linspace(0, 2*pi, 100);
y = sin(x);
plot(x, y);
title('Sine Wave');
saveas(gcf, 'sine_wave.png');
exit;

