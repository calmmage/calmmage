import {NextRequest, NextResponse} from "next/server"

export function middleware(request: NextRequest) {
  const locale = request.nextUrl.pathname.startsWith("/ru") ? "ru" : "en"
  const headers = new Headers(request.headers)
  headers.set("x-locale", locale)
  return NextResponse.next({
    request: {headers},
  })
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico|.*\\..*).*)"],
}
