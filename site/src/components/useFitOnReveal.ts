import { useEffect, useRef } from 'react';
import { useReactFlow } from 'reactflow';

/** Re-fit a graph the first time it actually has room.
 *
 * A tab panel is `display:none` until it is chosen, so a graph mounted inside one lays out
 * at zero by zero and its initial `fitView` has nothing to fit — the reader switches to the
 * tab and finds a blank canvas, or one node at 200% zoom. Watching the container rather than
 * the tab state keeps this independent of how the panel is hidden.
 *
 * Must be called inside a ReactFlowProvider. Attach the returned ref to the element that
 * wraps the ReactFlow canvas.
 *
 * `refitOnResize` keeps fitting while the box is still settling. The one-shot fit takes the
 * first non-zero size it is offered, and on a page whose surrounding layout is still
 * resolving that size is not the final one: the claim graph fitted at roughly half its
 * eventual width and sat at 26% zoom in a pane that had room for 51%. Opt in where the
 * container can change size after it appears; a reader who has zoomed or panned is left
 * alone, because refitting under someone who has taken hold of the canvas is worse than a
 * bad first fit. */
export function useFitOnReveal<T extends HTMLElement>(
  padding = 0.1,
  { refitOnResize = false }: { refitOnResize?: boolean } = {},
) {
  const ref = useRef<T>(null);
  const done = useRef(false);
  const size = useRef('');
  const { fitView } = useReactFlow();

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    let timer: ReturnType<typeof setTimeout>;
    const observer = new ResizeObserver(() => {
      if (done.current || !el.clientWidth || !el.clientHeight) return;
      const key = `${el.clientWidth}x${el.clientHeight}`;
      if (key === size.current) return;
      size.current = key;
      if (!refitOnResize) done.current = true;
      clearTimeout(timer);
      // After paint: fitView reads the viewport, which is not final in the same frame the
      // panel becomes visible.
      timer = setTimeout(() => requestAnimationFrame(() => fitView({ padding })), refitOnResize ? 90 : 0);
    });
    observer.observe(el);
    return () => { observer.disconnect(); clearTimeout(timer); };
  }, [fitView, padding, refitOnResize]);

  // Call when the reader takes hold of the canvas, so no later resize yanks it back.
  return Object.assign(ref, { settle: () => { done.current = true; } });
}
