def predict_reduction_suggestions(emissions, transport=None, energy=None):
    # Validate input
    if not isinstance(emissions, dict) or 'breakdown' not in emissions:
        return ["Invalid emissions data. Please provide a breakdown."]

    breakdown = emissions["breakdown"]
    if not breakdown or not all(key in breakdown for key in ["transport", "energy", "diet"]):
        return ["Breakdown must include transport, energy, and diet categories."]

    # Find the category with the highest emissions
    max_value = max(breakdown.values())
    max_categories = [category for category, value in breakdown.items() if value == max_value]
    # If there's a tie, prioritize transport > energy > diet
    max_category = max_categories[0] if len(max_categories) == 1 else (
        "transport" if "transport" in max_categories else
        "energy" if "energy" in max_categories else "diet"
    )

    suggestions = []

    # Add range-specific suggestions based on transport and energy values
    if max_category == "transport":
        if transport is not None:
            if transport < 50:
                suggestions.extend([
                    "Great job on low mileage! Consider walking or biking for short trips.",
                    "Use a bike-sharing program to maintain your low transport emissions."
                ])
            elif transport >= 1000:
                suggestions.extend([
                    "Your high mileage is a major contributor—switch to public transit for long trips.",
                    "Consider an electric vehicle to drastically cut transport emissions."
                ])
            else:
                suggestions.extend([
                    "Carpool with colleagues to reduce your transport emissions.",
                    "Switch to a hybrid vehicle to lower your carbon footprint."
                ])
        else:
            suggestions.extend([
                "Consider using public transportation or carpooling.",
                "Switch to an electric vehicle if possible."
            ])
    elif max_category == "energy":
        if energy is not None:
            if energy < 100:
                suggestions.extend([
                    "Excellent low energy usage! Unplug devices to avoid phantom loads.",
                    "Use energy-efficient lighting like LEDs to maintain low usage."
                ])
            elif energy >= 3000:
                suggestions.extend([
                    "Your high energy use is significant—install solar panels to offset it.",
                    "Conduct an energy audit to identify and reduce high usage areas."
                ])
            else:
                suggestions.extend([
                    "Switch to energy-efficient appliances to lower usage.",
                    "Install a programmable thermostat to save energy."
                ])
        else:
            suggestions.extend([
                "Switch to energy-efficient appliances.",
                "Use renewable energy sources like solar power."
            ])
    elif max_category == "diet":
        suggestions.extend([
            "Reduce meat consumption and try plant-based meals.",
            "Support local and sustainable food sources."
        ])

    return suggestions[:2]  # Limit to 2 suggestions