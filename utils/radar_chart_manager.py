# utils/radar_chart_manager.py

import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import math

class RadarChartManager:
    def get_metric_data(self, tickers, metrics):
        """
        Retrieve multiple metrics for each ticker using yfinance.
        Returns:
           data: A dict of the form:
                 {
                   'AAPL': {'trailingPE': 25.0, 'dividendYield': 0.005, ...},
                   'TSLA': {...},
                   ...
                 }
           warning_message: A string if some tickers/metrics fail, else None.
        """
        data = {}
        failed_tickers = []

        for ticker in tickers:
            # Initialize per-ticker dict
            data[ticker.upper()] = {}
            try:
                stock = yf.Ticker(ticker)
                info = stock.info

                for metric in metrics:
                    val = info.get(metric, None)
                    if val is None or pd.isna(val):
                        data[ticker.upper()][metric] = None
                    else:
                        data[ticker.upper()][metric] = val

            except Exception:
                # If any error occurs for the entire ticker
                failed_tickers.append(ticker)
                data[ticker.upper()] = {}

        # Remove tickers that have no data at all
        for t in list(data.keys()):
            # if everything is None or the dict is empty
            if not any(v is not None for v in data[t].values()):
                data.pop(t)

        if len(data) == 0:
            # no successful data
            return None, "No valid data could be fetched for the requested tickers."

        warning_message = None
        if len(failed_tickers) > 0:
            warning_message = (
                f"Warning: Unable to retrieve data for {', '.join(failed_tickers)}. "
                f"Proceeding with {', '.join(data.keys())}."
            )

        return data, warning_message


    def create_radar_chart(self, data, metrics, normalize=False):
        """
        Creates a radar chart from `data`, where
            data = {
              'TICKER1': {metric1: val, metric2: val2, ...},
              'TICKER2': {...}, ...
            }
        The `metrics` list is the set of metrics to display.
        
        If multiple metrics are provided, each ticker is its own trace, 
        and the categories are the metrics.
        
        If there is only one metric, 
        then the categories become the tickers, and we have a single trace.
        
        `normalize` can be True if you want to do a min-max normalization 
        on each metric to [0, 1] in the multi-metric scenario.
        """
        tickers = list(data.keys())
        
        # 1) Handle the single-metric scenario (metrics = ["PE"], multiple tickers).
        if len(metrics) == 1:
            single_metric = metrics[0]
            # The categories will be each ticker
            categories = tickers[:]
            # The values for each ticker in order
            values = [
                data[t].get(single_metric, 0) if data[t].get(single_metric) is not None else 0 
                for t in tickers
            ]
            # Close the loop for Plotly
            categories += [categories[0]]
            values += [values[0]]

            fig = go.Figure()
            fig.add_trace(
                go.Scatterpolar(
                    r=values,
                    theta=categories,
                    fill='toself',
                    name=single_metric
                )
            )
            fig.update_layout(
                template='plotly_dark',
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        showticklabels=True
                    )
                ),
                showlegend=True,
                title=f"Radar Chart for {single_metric} across {', '.join(tickers)}"
            )
            return fig

        # 2) Otherwise, we have multiple metrics. The categories = metrics.
        #    Each ticker is its own trace.
        # Create a DataFrame from the data dict
        df = pd.DataFrame.from_dict(data, orient='index')  # shape: T x M
        # Ensure we only keep the requested metrics (and in the correct order)
        df = df[metrics]

        # Optionally do min-max normalization for each metric
        if normalize:
            for m in metrics:
                col = df[m]
                min_val = col.min()
                max_val = col.max()
                if min_val is not None and max_val is not None and max_val != min_val:
                    df[m] = (col - min_val) / (max_val - min_val)
                else:
                    # if no variation, set to zero
                    df[m] = 0

        fig = go.Figure()
        for ticker in df.index:
            row_vals = df.loc[ticker].fillna(0).values.tolist()
            # Close the loop
            fig.add_trace(
                go.Scatterpolar(
                    r=row_vals + [row_vals[0]],
                    theta=metrics + [metrics[0]],
                    fill='toself',
                    name=ticker
                )
            )

        fig.update_layout(
            template='plotly_dark',
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    showticklabels=True
                )
            ),
            showlegend=True,
            title="Radar Chart Comparison"
        )
        return fig
