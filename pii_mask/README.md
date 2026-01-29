# PII Mask UDF

This example demonstrates a Python UDF that anonymizes Personally
Identifiable Information (PII) such as names, phone numbers, email
addresses, credit card numbers, etc. in text using Microsoft Presidio
and spaCy's `en_core_web_sm` model and anonymizes them by masking the
detected entities with `******`.

This example shows how to include a "private" Python dependency that
is not on public PyPI.


## Files

- `src/pii_mask/__init__.py` - The UDF implementation that masks PII

- `pyproject.toml` - Project configuration and dependencies; note that
  this explains how to bring in private packages, like we'll need
  `en_core_web_sm` in this case


## Private Dependencies

This example requires the spaCy's English language model, which is
downloaded separately and so is not available on public PyPI. To
include it:

1. Download your dependency locally as a wheel or sdist file.

2. Add it as a dev dependency to your uv project.

   ```
   uv add --dev ./en_core_web_sm-3.8.0-py3-none-any.whl
   ```

   This will cause it to be a dev dependency and to have a custom
   "sources" location which is the local filesystem.

   > [!NOTE]
   >
   > Do not add your package as a non-dev dependency, nor specify the
   > requirement as anything but a local file.

3. Build your UDF package as described in the [project-level
   README](../../README.md).

   ```
   uv build --sdist
   ```

4. Create the artifact by zipping both your sdist and the private
   dependencies together inside.

   ```
   zip -FS -j dist/pii_mask-0.1.0.zip \
     dist/pii_mask-0.1.0.tar.gz \
     ./en_core_web_sm-3.8.0-py3-none-any.whl
   ```

5. Upload that artifact. Confluent Cloud will install the other
   package into the local Python virtualenv when running the UDF code.


## Notes

With larger models or dependencies, you may need to contact Confluent
to increase the size of the instance that runs your UDF.
