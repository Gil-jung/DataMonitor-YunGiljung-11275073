from monitor import apply_filter, apply_sort, diff_changed_ids, summarize


def orders():
    return [
        {"order_id": "o1", "status": "PAID", "amount": 100, "created_at": "2026-07-15T00:00:01"},
        {"order_id": "o2", "status": "CREATED", "amount": 200, "created_at": "2026-07-15T00:00:02"},
        {"order_id": "o3", "status": "PAID", "amount": 300, "created_at": "2026-07-15T00:00:00"},
    ]


def test_summarize_counts_total_and_by_status():
    summary = summarize(orders())

    assert summary["total"] == 3
    assert summary["by_status"]["PAID"] == 2
    assert summary["by_status"]["CREATED"] == 1


def test_summarize_empty_snapshot():
    summary = summarize([])

    assert summary["total"] == 0
    assert summary["by_status"] == {}


def test_apply_filter_matches_status():
    filtered = apply_filter(orders(), "status=PAID")

    assert {o["order_id"] for o in filtered} == {"o1", "o3"}


def test_apply_filter_none_returns_all():
    assert apply_filter(orders(), None) == orders()


def test_apply_sort_orders_by_key_ascending():
    sorted_orders = apply_sort(orders(), "created_at")

    assert [o["order_id"] for o in sorted_orders] == ["o3", "o1", "o2"]


def test_apply_sort_none_preserves_order():
    assert apply_sort(orders(), None) == orders()


def test_diff_changed_ids_detects_new_and_modified_orders():
    prev = [{"order_id": "o1", "status": "CREATED"}]
    current = [
        {"order_id": "o1", "status": "PAID"},
        {"order_id": "o2", "status": "CREATED"},
    ]

    changed = diff_changed_ids(prev, current)

    assert changed == {"o1", "o2"}


def test_diff_changed_ids_no_change_returns_empty_set():
    prev = [{"order_id": "o1", "status": "CREATED"}]
    current = [{"order_id": "o1", "status": "CREATED"}]

    assert diff_changed_ids(prev, current) == set()
