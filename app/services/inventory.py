from typing import Optional

CAPABILITIES = {
	"real_time_stock_tracking": "Real-time stock tracking across locations with low-stock and overstock alerts.",
	"automated_order_management": "Track purchase and sales orders centrally to reduce manual errors.",
	"smart_forecasting": "AI-driven demand prediction with seasonal and trend insights.",
	"multi_channel_integration": "Sync inventory with WhatsApp chatbot, online store, and accounting.",
	"reports_analytics": "Daily/weekly/monthly stock usage reports; detect slow/fast movers.",
}


FAQ_SNIPPETS = [
	(
		"inventory",
		"Invock provides real-time stock tracking, automated order management, AI forecasting, multi-channel sync, and analytics.",
	),
	(
		"stock",
		"We monitor stock across locations and alert on low/overstock.",
	), 
	(
		"forecast",
		"We offer AI-driven demand forecasting to avoid stock-outs.",
	),
	(
		"report",
		"You get daily/weekly/monthly reports and insights on item movement.",
	),
]


def answer_inventory_question(user_text: str) -> Optional[str]:
	text = (user_text or "").lower()
	keywords = [k for k, _ in FAQ_SNIPPETS]
	if any(k in text for k in keywords):
		for k, a in FAQ_SNIPPETS:
			if k in text:
				return a + "\n\nWould you like to set up a quick demo? I can take your details."
		# fallback generic inventory reply
		return (
			"Yes, we help with inventory management: real-time tracking, order management, AI forecasting, multi-channel sync, and analytics.\n\n"
			"Would you like to set up a quick demo? I can take your details."
		)
	return None
