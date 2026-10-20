var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();
app.MapGet("/", () => {
    var message = Environment.GetEnvironmentVariable("HEXON_MESSAGE");
    return Results.Json(new { app = "Hexon — .NET", configured = !string.IsNullOrEmpty(message), message = message ?? "HEXON_MESSAGE não definida" });
});
app.MapGet("/health", () => Results.Ok(new { status = "ok" }));
app.Run();
