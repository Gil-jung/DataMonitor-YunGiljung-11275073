def summarize(snapshot: list) -> dict:
    by_status: dict = {}
    for order in snapshot:
        by_status[order["status"]] = by_status.get(order["status"], 0) + 1
    return {"total": len(snapshot), "by_status": by_status}


def apply_filter(snapshot: list, filter_expr: str) -> list:
    if not filter_expr:
        return snapshot
    key, _, value = filter_expr.partition("=")
    return [order for order in snapshot if str(order.get(key)) == value]


def apply_sort(snapshot: list, sort_key: str) -> list:
    if not sort_key:
        return snapshot
    return sorted(snapshot, key=lambda order: order.get(sort_key))


def diff_changed_ids(prev_snapshot: list, snapshot: list) -> set:
    prev_by_id = {order["order_id"]: order for order in prev_snapshot}
    changed = set()
    for order in snapshot:
        order_id = order["order_id"]
        if order_id not in prev_by_id or prev_by_id[order_id] != order:
            changed.add(order_id)
    return changed
