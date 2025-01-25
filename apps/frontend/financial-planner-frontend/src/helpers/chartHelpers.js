// src/helpers/chartHelpers.js

import { baseChartOptions } from '../config/chartConfig';

export const createChartOptions = (title) => ({
  ...baseChartOptions,
  plugins: {
    ...baseChartOptions.plugins,
    title: {
      ...baseChartOptions.plugins.title,
      text: title,
    },
  },
});
