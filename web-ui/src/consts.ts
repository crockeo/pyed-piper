export const SERVER_URI = "http://localhost:3001";

export const GET_BUTTON_COUNT_URI = "/button/count";
export const GET_BUTTONS_URI = "/buttons";
export const GET_BUTTON_URI = "/button/{}";
export const PUT_BUTTON_URI = "/button/{}";

export const GET_SAMPLES_URI = "/samples";
export const GET_SAMPLE_URI = "/sample/{}";
export const POST_SAMPLE_URI = "/sample";

export function make_get_button_uri(index: number): string {
  return SERVER_URI + GET_BUTTON_URI.replace("{}", (index | 0).toString());
}

export function make_put_button_uri(index: number): string {
  return SERVER_URI + PUT_BUTTON_URI.replace("{}", (index | 0).toString());
}

export function make_get_sample_uri(uuid: string): string {
  return SERVER_URI + GET_SAMPLE_URI.replace("{}", uuid);
}
