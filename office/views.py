from django.shortcuts import render
import json


def index(request):
    items = [
        {
            "name": "Frozen Yogurt",
            "email": "test@test.com",
            "arrival": 6.0,
            "payout": 24,
            "office": 4.0,
            "status": "invitation pending",
        },
        {
            "name": "Ice cream sandwich",
            "email": "test@test.com",
            "arrival": 9.0,
            "payout": 37,
            "office": 4.3,
            "status": "invitation pending",
        },
        {
            "name": "Eclair",
            "email": "test@test.com",
            "arrival": 16.0,
            "payout": 23,
            "office": 6.0,
            "status": "active",
        },
        {
            "name": "Cupcake",
            "email": "test@test.com",
            "arrival": 3.7,
            "payout": 67,
            "office": 4.3,
            "status": "active",
        },
        {
            "name": "Gingerbread",
            "email": "test@test.com",
            "arrival": 16.0,
            "payout": 49,
            "office": 3.9,
            "status": "active",
        },
        {
            "name": "Jelly bean",
            "email": "test@test.com",
            "arrival": 0.0,
            "payout": 94,
            "office": 0.0,
            "status": "active",
        },
        {
            "name": "Lollipop",
            "email": "test@test.com",
            "arrival": 0.2,
            "payout": 98,
            "office": 0,
            "status": "active",
        },
        {
            "name": "Honeycomb",
            "email": "test@test.com",
            "arrival": 3.2,
            "payout": 87,
            "office": 6.5,
            "status": "active",
        },
        {
            "name": "Donut",
            "email": "test@test.com",
            "arrival": 25.0,
            "payout": 51,
            "office": 4.9,
            "status": "active",
        },
        {
            "name": "KitKat",
            "email": "test@test.com",
            "arrival": 26.0,
            "payout": 65,
            "office": 7,
            "status": "active",
        },
    ];
    context = {}
    context["items"] = json.dumps(items)
    return render(request, 'office.html', context)
