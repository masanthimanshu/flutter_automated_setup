import "package:dio/dio.dart";
import "package:flutter/material.dart";
import "package:hive_flutter/hive_flutter.dart";

import "endpoints.dart";
import "requests.dart";

final _hive = Hive.box("myBox");

class DioInterceptor extends Interceptor {
  const DioInterceptor({required this.dioHandler});

  final Dio dioHandler;

  @override
  void onRequest(options, handler) {
    options.headers.addAll({
      "Refresh": _hive.get("refreshToken"),
      "Authorization": _hive.get("authToken"),
    });

    super.onRequest(options, handler);
  }

  @override
  void onError(err, handler) async {
    final res = err.response?.data;
    final code = err.response?.statusCode;

    if (code == 401 && res["message"] == "Invalid token") {
      try {
        await _InterceptorMethods().refreshToken();
        handler.resolve(
          await _InterceptorMethods().retryRequest(
            err.requestOptions,
            dioHandler,
          ),
        );
      } catch (err) {
        debugPrint("Error occurred with Interceptor - $err");
        return null;
      }
    }

    super.onError(err, handler);
  }
}

class _InterceptorMethods with HTTPRequests {
  Future<void> refreshToken() async {
    final data = await getRequest(apiEndpoint(ApiEndpoints.refreshToken));
    if (data != null) _hive.put("authToken", data["authToken"]);
  }

  Future<Response<dynamic>> retryRequest(
    RequestOptions requestOptions,
    Dio dioHandler,
  ) async {
    final options = Options(
      method: requestOptions.method,
      headers: requestOptions.headers,
    );

    return dioHandler.request(
      options: options,
      requestOptions.path,
      data: requestOptions.data,
      queryParameters: requestOptions.queryParameters,
    );
  }
}
