from dexbot.strategies.config_parts.base_config import BaseConfig, ConfigElement

from dexbot.translator_strings import TranslatorStrings as TS

class StaggeredConfig(BaseConfig):
    @classmethod
    def configure(cls, return_base_config=True):
        """
        Modes description:

        Mountain:
        - Buy orders same QUOTE
        - Sell orders same BASE

        Neutral:
        - Buy orders lower_order_base * sqrt(1 + increment)
        - Sell orders higher_order_quote * sqrt(1 + increment)

        Valley:
        - Buy orders same BASE
        - Sell orders same QUOTE

        Buy slope:
        - All orders same BASE (profit comes in QUOTE)

        Sell slope:
        - All orders same QUOTE (profit made in BASE)
        """
        modes = [
            ('mountain', TS.staggered[0]), # Mountain
            ('neutral', TS.staggered[1]), # Neutral
            ('valley', TS.staggered[2]), # Valley
            ('buy_slope', TS.staggered[3]), # Buy Slope
            ('sell_slope', TS.staggered[4]), # Sell Slope
        ]

        return BaseConfig.configure(return_base_config) + [
            ConfigElement(
                'mode',
                'choice',
                'neutral',
                TS.staggered[5], # Strategy mode
                TS.staggered[6], # How to allocate funds and profits. Doesn't effect existing orders, only future ones
                modes,
            ),
            ConfigElement(
                'spread', 
                'float', 
                6, 
                TS.staggered[7], # Spread
                TS.staggered[8], # The percentage difference between buy and sell
                (0, None, 2, '%')
            ),
            ConfigElement(
                'increment',
                'float',
                4,
                TS.staggered[9], # Increment
                TS.staggered[10], # The percentage difference between staggered orders
                (0, None, 2, '%'),
            ),
            ConfigElement(
                'center_price_dynamic',
                'bool',
                True,
                TS.staggered[11], # Market center price
                TS.staggered[12], # Begin strategy with center price obtained from the market. Use with mature markets
                None,
            ),
            ConfigElement(
                'center_price',
                'float',
                0,
                TS.staggered[13], # Manual center price
                TS.staggered[14], # In an immature market, give a center price manually to begin with. BASE/QUOTE
                (0, 1000000000, 8, ''),
            ),
            ConfigElement(
                'lower_bound',
                'float',
                1,
                TS.staggered[15], # Lower bound
                TS.staggered[16], # The lowest price (Quote/Base) in the range
                (0, 1000000000, 8, ''),
            ),
            ConfigElement(
                'upper_bound',
                'float',
                1000000,
                TS.staggered[17], # Upper bound
                TS.staggered[18], # The highest price (Quote/Base) in the range
                (0, 1000000000, 8, ''),
            ),
            ConfigElement(
                'instant_fill', 
                'bool', 
                True, 
                TS.staggered[19], # Allow instant fill
                TS.staggered[20], # Allow to execute orders by market
                None
            ),
            ConfigElement(
                'operational_depth',
                'int',
                10,
                TS.staggered[21], # Operational depth
                TS.staggered[22], # Order depth to maintain on books
                (2, 9999999, None),
            ),
            ConfigElement(
                'enable_fallback_logic',
                'bool',
                True,
                TS.staggered[23], # Enable fallback logic
                TS.staggered[24], # When unable to close the spread, cancel lowest buy order and place closer buy order
                None,
            ),
            ConfigElement(
                'enable_stop_loss',
                'bool',
                False,
                TS.staggered[25], # Enable Stop Loss
                TS.staggered[26], # Stop Loss order placed when bid price comes near lower bound
                None,
            ),
            ConfigElement(
                'stop_loss_discount',
                'float',
                5,
                TS.staggered[27], # Stop Loss discount
                TS.staggered[28], # Discount percent, Stop Loss order price = bid price / (1 + discount percent)
                (0, None, 2, '%'),
            ),
            ConfigElement(
                'stop_loss_amount',
                'float',
                50,
                TS.staggered[29], # Stop Loss Amount
                TS.staggered[30], # Relative amount of QUOTE asset to sell at Stop Loss, percentage
                (0, None, 2, '%'),
            ),
        ]

    @classmethod
    def configure_details(cls, include_default_tabs=True):
        return BaseConfig.configure_details(include_default_tabs) + []
