import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { container, boxes } = body;

    if (!container || !boxes) {
      return NextResponse.json({ error: 'Missing container or boxes data' }, { status: 400 });
    }

    const flaskResponse = await fetch('http://127.0.0.1:5328/pack', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ container, boxes }),
    });

    if (!flaskResponse.ok) {
      const errorBody = await flaskResponse.text();
      console.error(`Flask server error: ${flaskResponse.status} ${flaskResponse.statusText}`, errorBody);
      return NextResponse.json({ error: 'Failed to get response from packing service', details: errorBody }, { status: flaskResponse.status });
    }

    const result = await flaskResponse.json();
    return NextResponse.json(result);

  } catch (error) {
    let errorMessage = 'An unknown error occurred.';
    if (error instanceof Error) {
        errorMessage = error.message;
    }
    console.error("API Error:", errorMessage);
    return NextResponse.json({ error: 'Failed to process request', details: errorMessage }, { status: 500 });
  }
}