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
 * wraps the ReactFlow canvas. */
export function useFitOnReveal<T extends HTMLElement>(padding = 0.1) {
  const ref = useRef<T>(null);
  const done = useRef(false);
  const { fitView } = useReactFlow();

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const observer = new ResizeObserver(() => {
      if (done.current || !el.clientWidth || !el.clientHeight) return;
      done.current = true;
      // After paint: fitView reads the viewport, which is not final in the same frame the
      // panel becomes visible.
      requestAnimationFrame(() => fitView({ padding }));
    });
    observer.observe(el);
    return () => observer.disconnect();
  }, [fitView, padding]);

  return ref;
}
