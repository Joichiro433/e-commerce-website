import pino from 'pino';

const labels = pino().levels.labels;
const logger = pino({
  level: 'info',
  mixin: (_, level) => {
    return { severity: labels[level].toUpperCase() };
  },
});

export default logger;
