from django.contrib import admin

# Register your models here.
from .models import WatchList, APILog
from admincharts.admin import AdminChartMixin
from django.db.models.functions import TruncDate
from django.db.models import Count

# @admin.register(WatchList)
# class WatchListAdmin(AdminChartMixin,admin.ModelAdmin):
#     list_display = ('user', 'base_currency', 'target_currency', 'created_at')
#     search_fields = ('user__username', 'base_currency', 'target_currency')
#     list_filter = ('base_currency', 'target_currency')
    
#     admin_chart_data = {
#         # Chart 3: 🌍 Top Watched Currency Pairs
#         'Top Watched Currency Pairs': {
#             'queryset': WatchList.objects.values('base_currency', 'target_currency')
#                 .annotate(total=Count('id')).order_by('-total')[:5],
#             'labels': lambda qs: [f"{entry['base_currency']}→{entry['target_currency']}" for entry in qs],
#             'values': lambda qs: [entry['total'] for entry in qs],
#             'chart_type': 'bar',
#         }
#     }
# def debug_qs_labels(qs):
#     data = list(qs)  # Force evaluation
#     print("📊 [DEBUG] WatchList chart queryset:")
#     for entry in data:
#         print(f"  - {entry['base_currency']} → {entry['target_currency']} = {entry['total']}")
#     return [f"{entry['base_currency']}→{entry['target_currency']}" for entry in data]

# def debug_qs_values(qs):
#     data = list(qs)
#     return [entry['total'] for entry in data]

# @admin.register(WatchList)
# class WatchListAdmin(AdminChartMixin, admin.ModelAdmin):
#     list_display = ('user', 'base_currency', 'target_currency', 'created_at')
#     search_fields = ('user__username', 'base_currency', 'target_currency')
#     list_filter = ('base_currency', 'target_currency')

#     def get_admin_chart_data(self, request):
#         qs = WatchList.objects.values('base_currency', 'target_currency') \
#                               .annotate(total=Count('id')) \
#                               .order_by('-total')[:5]
#         return {
#             # Chart 1: 🌍 Top Watched Currency Pairs
#             'Top Watched Currency Pairs': {
#                 'queryset': qs,
#                 'labels': debug_qs_labels,  # debug + labels
#                 'values': debug_qs_values,  # debug + values
#                 'chart_type': 'bar',
#             }
#         }
@admin.register(WatchList)
class WatchListAdmin(AdminChartMixin, admin.ModelAdmin):
    #change_list_template = "charts/change_list.html"
    list_display = ('user', 'base_currency', 'target_currency', 'created_at')
    search_fields = ('user__username', 'base_currency', 'target_currency')
    list_filter = ('base_currency', 'target_currency')

    

    def changelist_view(self, request, extra_context=None):
        queryset = WatchList.objects.values('base_currency', 'target_currency') \
            .annotate(total=Count('id')).order_by('-total')[:4]

        labels = [f"{entry['base_currency']}→{entry['target_currency']}" for entry in queryset]
        values = [entry['total'] for entry in queryset]

        # ✅ Debugging logs
        print("✅ queryset:", list(queryset))
        print("✅ labels:", labels)
        print("✅ values:", values)

        extra_context = extra_context or {}
        extra_context['admincharts'] = {
            'Top Watched Currency Pairs': {
                'type': 'bar',
                'labels': labels,
                'values': values,
                'options': {
                    'aspectRatio': 6,
                    'plugins': {
                        'legend': {'display': False}
                    }
                }
            }
        }

        return super().changelist_view(request, extra_context=extra_context)    


@admin.register(APILog)
class APILogAdmin(AdminChartMixin,admin.ModelAdmin):
    list_display = ('user', 'endpoint', 'method','status_code', 'timestamp','success', 'ip_address')
    list_filter = ('method', 'endpoint', 'user','status_code', 'success')
    search_fields = ('user__username', 'endpoint', 'ip_address')
    
    admin_chart_data = {
        # Chart 1: 📊 API Requests Per Day
        'API Requests Per Day': {
            'queryset': APILog.objects.all(),
            'date_field': 'timestamp',
            'aggregate': Count('id'),
            'group_by': TruncDate('timestamp'),
        },
        # Chart 2: 🧑‍💻 Top 5 Users by API Usage
        'Top 5 Users by API Usage': {
            'queryset': APILog.objects.values('user__username').annotate(total=Count('id')).order_by('-total')[:5],
            'labels': lambda qs: [entry['user__username'] or 'Anonymous' for entry in qs],
            'values': lambda qs: [entry['total'] for entry in qs],
            'chart_type': 'bar',
        },
        # Chart 4: 🥧 Status Code Pie Chart
        'Status Code Pie Chart': {
            'queryset': APILog.objects.values('status_code').annotate(count=Count('id')),
            'labels': lambda qs: [str(entry['status_code']) for entry in qs],
            'values': lambda qs: [entry['count'] for entry in qs],
            'chart_type': 'pie',
        },
    }



    