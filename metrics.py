import pandas as pd
import numpy as np

# assets




def compute_returns(prices: pd.DataFrame):
    returns = prices.pct_change()
    returns = returns.dropna()
    return returns

def compute_volatility(returns: pd.DataFrame):
    vol_daily = returns.std()
    vol_annual = returns.std() * (252**0.5)
    return vol_annual

def compute_cumulative_return(returns: pd.DataFrame):
    if returns.empty:
        return pd.Series(dtype=float)
    cumulative = (1 + returns).cumprod()
    result = cumulative.iloc[-1] - 1
    return result

def compute_var(returns: pd.DataFrame, level=5):
    # 1 day var 
    var = returns.quantile(level / 100)
    return var


def compute_drawdown(prices: pd.DataFrame):
    running_max = prices.cummax()
    drawdown = prices / running_max - 1
    max_drawdown = drawdown.min()
    return max_drawdown

def compute_correlation(returns: pd.DataFrame):
    corr = returns.corr()
    return corr

def compute_sharpe_ratio(returns :pd.DataFrame):
    # annuel 
    sharpe_ratio = (returns.mean()/ returns.std()) * (252**0.5)
    return sharpe_ratio





#poportfolio





def compute_portfolio_returns(returns: pd.DataFrame, weights):
    portfolio_returns = returns.dot(weights)

    return portfolio_returns


def compute_portfolio_es(portfolio_returns, level=5):
    var = portfolio_returns.quantile(level/100)
    losses = portfolio_returns[portfolio_returns<=var]
    es = -losses.mean()
    return es 

    
    
def compute_portfolio_volatility(returns: pd.DataFrame, weights: pd.Series):
    
    cov_matrix = returns.cov()
    #σp2​=w⊤Σw
    variance = weights @ cov_matrix @ weights
    
    vol_daily = variance ** 0.5
    vol_annual = vol_daily * (252 ** 0.5)
    return vol_annual


def compute_portfolio_var(portfolio_returns, level=5):
    var_portefolio = -portfolio_returns.quantile(level/100) 
    # var 10 jour 
    return var_portefolio



def monte_carlo_portfolio(returns, weights, n_simulations=10000,level=5 ):
    mean = returns.mean()
    cov = returns.cov()
    
    simulated = np.random.multivariate_normal(mean, cov, n_simulations)
    
    portfolio_simulated = simulated.dot(weights)
    
    quantile = np.quantile(portfolio_simulated, level/100)
    var = -quantile
    losses = portfolio_simulated[portfolio_simulated <= quantile]
    es = -losses.mean()
    
    return var, es, portfolio_simulated
 