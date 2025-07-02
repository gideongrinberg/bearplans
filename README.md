# Bearplans

This web app allows a student to select the courses they wish to take and then generates every possible schedule based on the available sections of that course. I built part of this project for HackClub's [Summer of Making](https://summer.hackclub.com) event.

## AI Acknowledgement

I used Claude to do some styling and build the calendar component (app/src/routes/schedule/Schedule.svelte).

> [!NOTE] 
> The subsequent information was copied directly from the SvelteKit template readme

## Developing

Once you've created a project and installed dependencies with `npm install` (or `pnpm install` or `yarn`), start a development server:

```bash
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

## Building

To create a production version of your app:

```bash
npm run build
```

You can preview the production build with `npm run preview`.

> To deploy your app, you may need to install an [adapter](https://svelte.dev/docs/kit/adapters) for your target environment.
